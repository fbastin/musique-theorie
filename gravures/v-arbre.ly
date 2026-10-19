\version "2.24.3"
%% Fichier produit par outils/generer_valeurs.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new StaffGroup \with { \override StaffGrouper.staff-staff-spacing = #'((basic-distance . 7) (minimum-distance . 6) (padding . 1)) } <<
    \new RhythmicStaff \with { instrumentName = \markup \small \italic "1 ronde" } {
      \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      a'1
      \bar "|."
    }
    \new RhythmicStaff \with { instrumentName = \markup \small \italic "2 blanches" } {
      \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      a'2 a'2
      \bar "|."
    }
    \new RhythmicStaff \with { instrumentName = \markup \small \italic "4 noires" } {
      \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      a'4 a'4 a'4 a'4
      \bar "|."
    }
    \new RhythmicStaff \with { instrumentName = \markup \small \italic "8 croches" } {
      \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      a'8[ a'8] a'8[ a'8] a'8[ a'8] a'8[ a'8]
      \bar "|."
    }
    \new RhythmicStaff \with { instrumentName = \markup \small \italic "16 doubles" } {
      \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      a'16[ a'16 a'16 a'16] a'16[ a'16 a'16 a'16] a'16[ a'16 a'16 a'16] a'16[ a'16 a'16 a'16]
      \bar "|."
    }
  >>
  \layout {
    indent = 18\mm line-width = 300\mm
    \context { \Score proportionalNotationDuration = #(ly:make-moment 1/24) \markLengthOn \override SpacingSpanner.uniform-stretching = ##t }
  }
}
