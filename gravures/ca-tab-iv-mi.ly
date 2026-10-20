\version "2.24.3"
%% Fichier produit par outils/generer_cadences.py — ne pas modifier à la main.
#(set-global-staff-size 13)
\paper {
  indent = 0
  ragged-right = ##f
  paper-width = 168\mm
  line-width = 166\mm
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
  \new PianoStaff <<
    \new Lyrics = "noms"
    \new Lyrics = "positions"
    \new Staff = "haut" { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "md" { \key e \major <gis' b' e''>1 <a' cis'' e''>1 <fis' b' dis''>1 <gis' b' e''>1 \bar "|"  <b e' gis'>1 <cis' e' a'>1 <b dis' fis'>1 <b e' gis'>1 \bar "|"  <e' gis' b'>1 <e' a' cis''>1 <dis' fis' b'>1 <e' gis' b'>1 \bar "||" \key e \minor <g' b' e''>1 <a' c'' e''>1 <fis' b' dis''>1 <g' b' e''>1 \bar "|"  <b e' g'>1 <c' e' a'>1 <b dis' fis'>1 <b e' g'>1 \bar "|"  <e' g' b'>1 <e' a' c''>1 <dis' fis' b'>1 <e' g' b'>1 \bar "|." } }
    \new Staff { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key e \major e,1 a,1 b,1 e,1 \bar "|"  e,1 a,1 b,1 e,1 \bar "|"  e,1 a,1 b,1 e,1 \bar "||" \key e \minor e,1 a,1 b,1 e,1 \bar "|"  e,1 a,1 b,1 e,1 \bar "|"  e,1 a,1 b,1 e,1 \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { \markup \tiny \italic "mi majeur" _ _ _ _ _ _ _ _ _ _ _ \markup \tiny \italic "mi mineur" _ _ _ _ _ _ _ _ _ _ _ }
    \context Lyrics = "positions" \lyricsto "md" { \markup \tiny \italic "octave" _ _ _ \markup \tiny \italic "tierce" _ _ _ \markup \tiny \italic "quinte" _ _ _ \markup \tiny \italic "octave" _ _ _ \markup \tiny \italic "tierce" _ _ _ \markup \tiny \italic "quinte" _ _ _ }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #1.0
    }
    \context {
      \Lyrics
      \override LyricText.self-alignment-X = #LEFT
      \override LyricText.extra-spacing-width = #'(+inf.0 . -inf.0)
      \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #0.2
      \override VerticalAxisGroup.nonstaff-nonstaff-spacing.padding = #0.1
    }
  }
}
