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
  \new StaffGroup <<
    \new Staff \with { instrumentName = \markup \small \italic "avec point" } {
      \clef treble \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      \textMark \markup \small \italic "blanche pointée" a'2. \bar "|" \textMark \markup \small \italic "noire pointée" a'4. \bar "|" \textMark \markup \small \italic "croche pointée" a'8. \bar "|" \textMark \markup \small \italic "blanche doublement pointée" a'2.. \bar "|" \textMark \markup \small \italic "soupir pointé" r4.
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic "sans point" } {
      \clef treble \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      a'2~ a'4 \bar "|" a'4~ a'8 \bar "|" a'8[~ a'16] \bar "|" a'2~ a'4~ a'8 \bar "|" r4 r8
      \bar "|."
    }
  >>
  \layout {
    indent = 18\mm line-width = 300\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \markLengthOn \override TextMark.self-alignment-X = #LEFT }
  }
}
