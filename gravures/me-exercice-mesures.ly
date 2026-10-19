\version "2.24.3"
%% Fichier produit par outils/generer_mesure.py — ne pas modifier à la main.
\paper {
  indent = 0
  paper-width = 152\mm
  line-width = 150\mm
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
  \new Staff { \new Voice {
        \clef treble \autoBeamOff \numericTimeSignature \omit Staff.TimeSignature \override TextScript.staff-padding = #2.5
        \time 6/8 e''8[^\markup \small \bold 1 d''8 c''8] d''4. | \time 3/4 g'4^\markup \small \bold 2 a'8[ b'8] c''8[ d''8] | \time 2/4 a'4^\markup \small \bold 3 g'8[ f'8] | \time 9/8 g'4.^\markup \small \bold 4 a'4 g'8 f'4. | \time 4/4 c''4^\markup \small \bold 5 d''8[ e''8] f''4 g''4 | \time 12/8 e''8[^\markup \small \bold 6 f''8 g''8] a''4. g''8[ f''8 e''8] d''4. | \time 3/4 r4^\markup \small \bold 7 c''4 c''4 | \time 6/8 c''8[^\markup \small \bold 8 d''8 e''8] f''4 r8 | \time 3/8 g'8[^\markup \small \bold 9 a'8 b'8]
        \bar "|."
      } }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
